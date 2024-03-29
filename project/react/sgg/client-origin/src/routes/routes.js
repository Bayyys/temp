import { Navigate } from "react-router-dom";
import Login from "../pages/Login/Login";
import Admin from "../pages/Admin/Admin";
import Home from "../pages/Home/Home";
import Category from "../pages/Category/Category";
import Product from "../pages/Product/Product";
import User from "../pages/User/User";
import Role from "../pages/Role/Role";
import Bar from "../pages/Charts/Bar";
import Line from "../pages/Charts/Line";
import Pie from "../pages/Charts/Pie";
import Order from "../pages/Order/Order";

const routes = [
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <Admin />,
    items: [
      {
        path: "",
        element: <Navigate to="/home" />,
      },
      {
        path: "home",
        element: <Home />,
      },
      {
        path: "category",
        element: <Category />,
      },
      {
        path: "product",
        element: <Product />,
      },
      {
        path: "user",
        element: <User />,
      },
      {
        path: "role",
        element: <Role />,
      },
      {
        path: "charts",
        items: [
          {
            path: "",
            element: <Navigate to="/charts/bar" />,
          },
          {
            path: "bar",
            element: <Bar />,
          },
          {
            path: "line",
            element: <Line />,
          },
          {
            path: "pie",
            element: <Pie />,
          },
          {
            path: "*",
            element: <Navigate to="/404" />,
          },
        ],
      },
      {
        path: "order",
        element: <Order />,
      },
    ],
  },
];

export default routes;
