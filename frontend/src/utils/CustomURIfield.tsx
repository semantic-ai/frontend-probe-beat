import { FC } from "react";
import { DateFieldProps, FunctionField } from "react-admin";

export const CustomURIfield: FC<DateFieldProps> = (props) => {
  return (
    <FunctionField
      render={(record: any) => record[props.source!].split("/").slice(-1)}
    />
  );
};
