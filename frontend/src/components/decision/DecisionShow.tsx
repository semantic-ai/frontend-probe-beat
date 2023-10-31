import React, { FC } from "react";
import {
  Show,
  ShowProps,
  TextField,
  RichTextField,
  SimpleShowLayout,
  Datagrid,
  ReferenceManyField,
  useRedirect,
  useRecordContext,
  Button,
  Labeled,
  useGetOne,
  Loading,
  EditButton,
} from "react-admin";
import { Grid, Stack } from "@mui/material";
import { ArticleField } from "../article/ArticleField";
import { MotivationField } from "../motivation/MotivationField";
import { LabelChipList } from "../label/LabelChipList";
import EditIcon from "@mui/icons-material/Edit";
import { CustomDateField } from "../../utils/CustomDateField";
import { CustomURIfield } from "../../utils/CustomURIfield";

const AnnotateButton = (props) => {
  const redirect = useRedirect();
  const record = useRecordContext();

  return (
    <Button
      label="Annotate"
      onClick={() => {
        redirect(`/annotations/create?source={"decision_id":"${record.id}"}`);
      }}
    />
  );
};

const ArticleFieldWrapper = (props) => {
  const record = useRecordContext();

  return (
    <Labeled>
      <ArticleField data={record.articles} label={"Articles"} />
    </Labeled>
  );
};

const MotivationFieldWrapper = (props) => {
  const record = useRecordContext();

  return (
    <Labeled>
      <MotivationField text={record.motivation} label={"Motivation"} />
    </Labeled>
  );
};

const AnnotationPanel = () => {
  const record = useRecordContext();
  const { data: taxonomy, isLoading } = useGetOne(
    "taxonomies",
    { id: record.taxonomy_id },
    { enabled: record.taxonomy_id !== undefined }
  );
  if (!taxonomy) {
    return <></>;
  }
  if (isLoading) {
    return <Loading />;
  }
  return <LabelChipList tree={taxonomy["tree"]} labels={record.labels} />;
};

const AnnotationAnnotateButton = (prop) => {
  const record = useRecordContext();
  const redirect = useRedirect();
  if (!record) {
    return <></>;
  }
  const path = `/annotations/create?source={"decision_id":"${record.decision_id}", "taxonomy_id":"${record.taxonomy_id}", "labels":"${record.labels}"}`;
  return (
    <Button
      label="Edit"
      onClick={() => redirect(path)}
      children={<EditIcon />}
    />
  );
};

const AnnotationRowSx = (record, index) => ({
  backgroundColor: record.user ? "#efe" : "white",
});

export const DecisionShow: FC<ShowProps> = (props) => {
  return (
    <Show>
      <Grid container spacing={2} alignItems="flex-start">
        <Grid container item xs={2} sm={3} md={3} lg={4} xl={6}>
          <SimpleShowLayout>
            <TextField source="id" label="URI" />
            <TextField source="portal_link" label="Portal link" />
            <TextField source="short_title" />
            <ArticleFieldWrapper />
            <MotivationFieldWrapper />
            <RichTextField source="description" />
          </SimpleShowLayout>
        </Grid>
        <Grid container item xs={6} sm={6} md={6} lg={6} xl={6}>
          <Stack>
            <AnnotateButton />
            <ReferenceManyField
              label="annotations"
              reference="annotations"
              target="decision_id"
            >
              <Datagrid
                expand={<AnnotationPanel />}
                bulkActionButtons={false}
                rowSx={AnnotationRowSx}
              >
                <AnnotationAnnotateButton />
                <CustomURIfield source="taxonomy_id" sortable={false} />
                <TextField source="annotator" sortable={false} />
                <CustomDateField source="date" sortable={false} />
              </Datagrid>
            </ReferenceManyField>
          </Stack>
        </Grid>
      </Grid>
    </Show>
  );
};
