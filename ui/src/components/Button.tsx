import { ReactNode } from "react";

export default function Button(props: {
  onclick: Function;
  children: ReactNode;
  params?: object;
}) {
  const { onclick, children, params } = props;

  const handleCallAction = async () => {
    try {
      const response = await onclick(params);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  return <button onClick={handleCallAction}>{children}</button>;
}
