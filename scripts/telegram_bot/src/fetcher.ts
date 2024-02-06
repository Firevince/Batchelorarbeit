const fetch = require('node-fetch');
import { config } from "./config";

export const fetchUrlBySearchQuery = async (query: string) => {
  const response = await fetch(`${config.BASE_URL}/api?text=${query}`);
  const data = await response.json() as any;
  const audioUrl = config.BASE_URL + data?.url;
  console.log(audioUrl);
  return audioUrl;
};
