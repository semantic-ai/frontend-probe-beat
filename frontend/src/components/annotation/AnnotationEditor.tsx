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
  useNotify,
  Toolbar,
  SaveButton,
} from "react-admin";
import { Grid, Typography, Stack } from "@mui/material";
import { useFormContext } from "react-hook-form";
import purify from "dompurify";
import { ArticleField } from "../article/ArticleField";
import { MotivationField } from "../motivation/MotivationField";
import { LabelChipList } from "../label/LabelChipList";
import { LabelButton } from "./LabelButton";

import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";

const LabelAutocomplete = (prop) => {
  var options = [];
  Object.keys(prop.tree).map(
    (key) =>
      (options = options.concat(
        prop.tree[key].map((element) => {
          element.parent = key;
          return element;
        })
      ))
  );

  const { setValue, getValues } = useFormContext();
  const notify = useNotify();

  const addLabel = (element) => {
    if (element) {
      var labels = getValues("labels") || [];
      if (labels.map((item) => item).includes(element.id)) {
        notify(`Label already selected`, { type: "info" });
      } else {
        labels.push(element.id);
        setValue("labels", labels);
      }
    }
  };

  const getNameOnIndex = (id) => {
    const element = options.filter((element) => element.id == id)[0];
    if (element && element != "top level") {
      return element.name + " | ";
    }
    return "";
  };

  options = options.map((element) => {
    element.display_name = `${getNameOnIndex(element.parent)}${element.name}`;
    return element;
  });

  return (
    <Autocomplete
      disablePortal
      id="labelAutocomplete"
      options={options}
      getOptionLabel={(option) => option.display_name}
      renderInput={(params) => <TextField {...params} label="Search label" />}
      onChange={(event, value) => {
        addLabel(value);
      }}
    />
  );
};

const LabelChipListWrapper = (prop) => {
  const { setValue, getValues } = useFormContext();
  var labels = getValues("labels") || [];
  if (typeof labels === "string" || labels instanceof String) {
    labels = labels.split(",");
    setValue("labels", labels);
  }
  const onDeleteGenerator = (item) => {
    return () => {
      const filtered_labels = labels.filter((l) => l !== item);
      setValue("labels", filtered_labels);
    };
  };

  return (
    <LabelChipList
      tree={prop.tree}
      labels={labels}
      onDeleteGenerator={onDeleteGenerator}
    />
  );
};

const AnnotationToolbar = (args, props) => {
  const redirect = useRedirect();
  const notify = useNotify();
  const record = useRecordContext();

  return (
    <Toolbar {...props}>
      <SaveButton
        alwaysEnable
        label="Save and open decision"
        mutationOptions={{
          onSuccess: () => {
            notify("Annotation saved");
            redirect(
              `/decisions/${encodeURIComponent(
                record.decision_id.toString()
              )}/show`
            );
          },
        }}
        type="button"
      />
      <SaveButton
        alwaysEnable
        label="Save and go to list"
        mutationOptions={{
          onSuccess: () => {
            notify("Annotation saved");
            redirect("/decisions");
          },
        }}
        type="button"
        variant="text"
      />
    </Toolbar>
  );
};

const validateAnnotationCreation = (values) => {
  const errors = {};
  if (!values.labels || values.labels.length == 0) {
    errors["taxonomy_id"] = "Empty labels are not allowed";
  }
  return errors;
};

export const AnnotationEditor = (props) => {
  return (
    <SimpleForm
      toolbar={<AnnotationToolbar />}
      validate={validateAnnotationCreation}
    >
      <Grid container spacing={2} alignItems="flex-start">
        <Grid container item xs={6} sm={6} md={6} lg={6} xl={6}>
          {/* hidden TextInput to capture id of decision annotating */}
          <TextInput
            source="decision_id"
            disabled={true}
            style={{ display: "none" }}
          />
          <FormDataConsumer>
            {({ formData, ...rest }) => {
              const { data: decision, isLoading } = useGetOne(
                "decisions",
                { id: formData.decision_id },
                { enabled: formData.decision_id !== undefined }
              );
              if (isLoading) {
                return <Loading />;
              }
              return (
                <Stack>
                  <Labeled label="URI">
                    <Typography component="span" variant="body2">
                      {decision.id}
                    </Typography>
                  </Labeled>
                  <Labeled label="Short title">
                    <Typography component="span" variant="body2">
                      {decision.short_title}
                    </Typography>
                  </Labeled>
                  <Labeled>
                    <ArticleField data={decision.articles} label={"Articles"} />
                  </Labeled>
                  <Labeled>
                    <MotivationField
                      text={decision.motivation}
                      label="Motivation"
                    />
                  </Labeled>
                  <Labeled label="Description">
                    <Typography
                      component="span"
                      variant="body2"
                      className="decription"
                    >
                      <span
                        dangerouslySetInnerHTML={{
                          __html: purify.sanitize(decision.description),
                        }}
                      />
                    </Typography>
                  </Labeled>
                </Stack>
              );
            }}
          </FormDataConsumer>
        </Grid>
        <Grid container item xs={6} sm={6} md={6} lg={6} xl={6}>
          <Stack>
            <FormDataConsumer>
              {({ formData, ...rest }) => {
                if (
                  formData.labels &&
                  formData.taxonomy_id &&
                  formData.labels.length > 0
                ) {
                  return (
                    <ReferenceInput
                      source="taxonomy_id"
                      reference="taxonomies"
                      filter={{ id: formData.taxonomy_id }}
                    >
                      <SelectInput
                        emptyText={
                          "verander taxonomy (deselecteer huidige labels)"
                        }
                      />
                    </ReferenceInput>
                  );
                }
                return (
                  <ReferenceInput source="taxonomy_id" reference="taxonomies">
                    <SelectInput />
                  </ReferenceInput>
                );
              }}
            </FormDataConsumer>
            <FormDataConsumer>
              {({ formData, ...rest }) => {
                const { setValue } = useFormContext();
                const { data: taxonomy, isLoading } = useGetOne(
                  "taxonomies",
                  { id: formData.taxonomy_id },
                  {
                    enabled:
                      formData.taxonomy_id != undefined ||
                      formData.taxonomy_id != null,
                  }
                );
                if (
                  formData.taxonomy_id == undefined ||
                  formData.taxonomy_id == null
                ) {
                  if (formData.labels != undefined) {
                    setValue("labels", undefined);
                  }
                  return <></>;
                }
                if (isLoading) {
                  return <Loading />;
                }
                if (taxonomy["tree"]) {
                  return (
                    <>
                      <LabelChipListWrapper tree={taxonomy["tree"]} />
                      <LabelAutocomplete tree={taxonomy["tree"]} />
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
                        {taxonomy["tree"]["top_level"].map((item, index) => (
                          <LabelButton
                            key={index}
                            id={item.id}
                            value={item.name}
                            tree={taxonomy["tree"]}
                          />
                        ))}
                      </Grid>
                    </>
                  );
                }
              }}
            </FormDataConsumer>
          </Stack>
        </Grid>
      </Grid>
    </SimpleForm>
  );
};
