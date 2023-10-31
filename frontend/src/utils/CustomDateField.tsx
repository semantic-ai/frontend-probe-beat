import { FC } from "react";
import { DateFieldProps, FunctionField } from "react-admin";
import moment from "moment-timezone";

export const CustomDateField: FC<DateFieldProps> = (props) => {
  return (
    <FunctionField
      render={(record: any) =>
        moment
          .utc(record[props.source!])
          .local()
          .format("MMMM Do YYYY, HH:mm:ss")
      }
    />
  );
};
