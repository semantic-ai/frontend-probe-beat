import { Grid } from "@mui/material";
import Chip from "@mui/material/Chip";

export const LabelChipList = (prop) => {
  const labels = prop.labels;
  if (!labels) return null;
  return (
    <Grid container item xs={12} sm={12} md={12} lg={12} xl={12}>
      {labels.map((item) => {
        // var current_parent = prop.tree.filter((parent, children) => children.includes(item))
        var current_parent_array = Object.keys(prop.tree).filter((id) =>
          prop.tree[id].map((l) => l.id).includes(item)
        );
        // Drop label if no current parent
        var current_parent = current_parent_array[0];
        if (current_parent == undefined) {
          return <></>;
        }

        var label_str = prop.tree[current_parent].filter(
          (l) => l.id == item
        )[0]["name"];
        while (current_parent != "top_level") {
          var new_parent = Object.keys(prop.tree).filter((id) =>
            prop.tree[id].map((l) => l.id).includes(current_parent)
          )[0];
          label_str =
            prop.tree[new_parent].filter((l) => l.id == current_parent)[0][
              "name"
            ] +
            " | " +
            label_str;
          current_parent = new_parent;
        }
        if (prop.onDeleteGenerator) {
          return (
            <Chip
              label={label_str}
              key={label_str}
              onDelete={prop.onDeleteGenerator(item)}
              color="secondary"
            />
          );
        } else {
          return <Chip label={label_str} key={label_str} color="secondary" />;
        }
      })}
    </Grid>
  );
};
