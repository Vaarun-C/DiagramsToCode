import axiosInstance from '@utils/axiosInstance';
import { isAxiosError } from 'axios';
// const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const URL = ''//

export const sendDiagrams = async (files:File[]) => {
  try {
    const response = await axiosInstance.post(URL, {files});
    const { data } = response;
    return data;
  } catch (error) {
    if (isAxiosError(error) && error.response) {
      const { status, errorCode, errorMessage } = error.response.data;
      return { status, errorCode, errorMessage };
    } else {
      console.error(error);
      return {
        status: 500,
        errorCode: 'POST_DIAGRAMS_ERROR',
        errorMessage: 'Please try again later.',
      };
    }
  }
};
