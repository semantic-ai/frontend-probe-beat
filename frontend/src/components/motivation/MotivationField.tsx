import * as React from "react";
import { Button, Loading } from "react-admin";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";

export const MotivationField = ({ text, label }) => {
  const [show, setShow] = React.useState(true);
  return (
    <>
      <Button
        label={show ? "show motivation" : "hide motivation"}
        onClick={() => setShow(!show)}
        style={{ width: "200px" }}
        children={show ? <VisibilityIcon /> : <VisibilityOffIcon />}
      />
      {show ? null : (
        <>
          <hr
            style={{
              background: "#003066",
              color: "#003066",
              borderColor: "#003066",
              height: "1px",
              width: "100%",
              opacity: "80%",
            }}
          />

          <div
            style={{
              width: "100%",
              maxHeight: "50vh",
              overflow: "scroll",
              backgroundColor: "rgba(200, 200, 200, 0.3)",
            }}
          >
            {!text
              ? null
              : text.split("\n").map((str, index) => <p key={index}>{str}</p>)}
          </div>

          <hr
            style={{
              background: "#003066",
              color: "#003066",
              borderColor: "#003066",
              height: "1px",
              width: "100%",
              opacity: "80%",
            }}
          />
        </>
      )}
    </>
  );
};
