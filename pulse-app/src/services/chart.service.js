import axios from "axios";
import { SERVER_BASE_URL } from "../common/consts/api";

export const getChartAvailableDates = async () => {
  const response = await axios.get(new URL("/dev/charts/available-dates", SERVER_BASE_URL).toString());
  // const response = await axios.get(new URL("/charts/available-dates", SERVER_BASE_URL).toString());
  console.log("getChartAvailableDates:", response.data);
  return response;
};

export const getChartByYear = async (year) => {
  // const response = await axios.get(new URL(`/charts?year=${year}`, SERVER_BASE_URL).toString());
  const response = await axios.get(new URL(`/dev/charts?year=${year}`, SERVER_BASE_URL).toString());
  console.log("getChartByYear:", response.data);
  return response;
};

export const getChartByDate = async (date) => {
  // const response = await axios.get(new URL(`/charts?date=${date}`, SERVER_BASE_URL).toString());
  const response = await axios.get(new URL(`/dev/charts?date=${date}`, SERVER_BASE_URL).toString());
  console.log("getChartByYear:", response.data);
  return response;
};