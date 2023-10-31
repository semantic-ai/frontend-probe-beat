import { Create, useNotify, useRedirect } from "react-admin";
import { AnnotationEditor } from "./AnnotationEditor";

export const AnnotationCreate = (props) => {
  const notify = useNotify();
  const redirect = useRedirect();

  const onSuccess = (data) => {
    notify(`Changes saved`);
    redirect(`/decisions`);
  };

  return (
    <Create mutationOptions={{ onSuccess }}>
      <AnnotationEditor />
    </Create>
  );
};
