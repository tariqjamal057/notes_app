import { configureStore } from "@reduxjs/toolkit";
import notesSlice from "./slicers/note";

const store = configureStore({
  reducer: {
    notes: notesSlice,
  },
});

export default store;
