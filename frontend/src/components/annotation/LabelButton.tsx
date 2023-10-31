import React from "react";
import {
  SimpleForm,
  Loading,
  ReferenceInput,
  FormDataConsumer,
  SelectInput,
  useGetOne,
  useRecordContext,
  useRedirect,
  TextInput,
  Labeled,
  Button,
  useNotify,
  Toolbar,
  SaveButton,
} from "react-admin";
import {
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { useFormContext } from "react-hook-form";
import ScaleText from "react-scale-text";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

export const LabelButton = (prop) => {
  const { setValue, getValues } = useFormContext();
  const notify = useNotify();

  // State for dialog
  const [open, setOpen] = React.useState(false);

  const close_function = () => {
    setOpen(false);
    if (prop.close_function) {
      prop.close_function();
    }
  };

  const addLabel = () => {
    var labels = getValues("labels") || [];
    if (labels.map((item) => item).includes(prop.id)) {
      notify(`Label already selected`, { type: "info" });
    } else {
      labels.push(prop.id);
      setValue("labels", labels);
    }
  };

  const children = prop.tree[prop.id];
  const has_children = children !== undefined;

  const onclick_function = () => {
    // If no children, add to annotations list or warn if already in list
    if (!has_children) {
      addLabel();
    }
    // Else, open pop-up window
    else {
      setOpen(true);
    }
  };

  return (
    <Grid item xs={12} sm={12} md={12} lg={6} xl={4}>
      <div
        style={{
          width: "100%",
          height: 100,
          alignItems: "center",
        }}
      >
        <ScaleText>
          <Button
            color="secondary"
            type="button"
            style={{
              width: "100%",
              height: 100,
              backgroundColor: "rgba(200, 200, 200, 0.3)",
            }}
            onClick={() => {
              onclick_function();
            }}
            label={prop.value}
            children={has_children ? <OpenInNewIcon /> : <AddIcon />}
          />
        </ScaleText>
      </div>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        aria-labelledby="form-dialog-title"
        maxWidth="sm"
        fullWidth={true}
        PaperProps={{
          style: {
            position: "absolute",
            right: 0,
            bottom: 0,
            minHeight: "80%",
            maxHeight: "80%",
          },
        }}
        sx={{
          backdropFilter: "blur(0px)",
          //other styles here
        }}
      >
        <DialogTitle id="form-dialog-title">{prop.value}</DialogTitle>
        <DialogActions>
          <Button
            label="Back"
            onClick={() => {
              setOpen(false);
            }}
            children={<ArrowBackIcon />}
            color="warning"
            style={{
              width: "33%",
              height: 50,
              backgroundColor: "rgba(200, 200, 200, 0.3)",
            }}
          />
          <Button
            label="Close"
            onClick={() => {
              close_function();
            }}
            children={<CloseIcon />}
            color="error"
            style={{
              width: "33%",
              height: 50,
              backgroundColor: "rgba(200, 200, 200, 0.3)",
            }}
          />
          <Button
            label="Select this label"
            onClick={() => {
              addLabel();
            }}
            children={<AddIcon />}
            color="secondary"
            style={{
              width: "33%",
              height: 50,
              backgroundColor: "rgba(200, 200, 200, 0.3)",
            }}
          />
        </DialogActions>
        <DialogContent>
          <Grid
            container
            item
            xs={12}
            sm={12}
            md={12}
            lg={12}
            xl={12}
            alignItems="flex-start"
            spacing={1}
          >
            {(children || []).map((item, index) => (
              <LabelButton
                key={index}
                id={item.id}
                value={item.name}
                close_function={close_function}
                tree={prop.tree}
              />
            ))}
          </Grid>
        </DialogContent>
      </Dialog>
    </Grid>
  );
};
