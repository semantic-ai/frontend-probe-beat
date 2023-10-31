import * as React from "react";
import Select from "react-select";

export const ArticleField = ({ data, label }) => {
  if (!data) {
    return <></>;
  }

  const options = data.map((item) => {
    return { value: item.id, label: item.number };
  });
  options.push({ value: "", label: "..." });

  const [selected, setSelected] = React.useState("");

  const textChange = (inputValue) => {
    setSelected(inputValue.value);
  };

  const selected_articles = data.filter((item) => item.id == selected);
  const text =
    selected_articles.length > 0 ? selected_articles[0]["content"] : "";

  return (
    <div style={{ width: "100%" }}>
      <Select options={options} onChange={textChange} />

      {
        // display lines if article is selected
        selected_articles.length > 0 ? (
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
              {text.split("\n").map((str, index) => (
                <p key={index}>{str}</p>
              ))}
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
        ) : null
      }
    </div>
  );
};
