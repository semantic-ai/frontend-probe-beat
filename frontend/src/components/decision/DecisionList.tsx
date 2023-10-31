import React, { FC } from "react";
import {
  Datagrid,
  List,
  ListProps,
  TextField,
  TextInput,
  SearchInput,
} from "react-admin";

const decisionFilters = [<SearchInput source="short_title" alwaysOn />];

const DecisionRowSx = (record, index) => ({
  backgroundColor: record.user_annotated ? "#efe" : "white",
});

export const DecisionList: FC<ListProps> = (
  props
) => (
  <List
    {...props}
    sort={{ field: "id", order: "DESC" }}
    filters={decisionFilters}
    perPage={25}
    exporter={false}
  >
    <Datagrid bulkActionButtons={false} rowClick={"show"} rowSx={DecisionRowSx}>
      <TextField source="id" sortable={false} />
      <TextField source="short_title" sortable={false} />
    </Datagrid>
  </List>
);
