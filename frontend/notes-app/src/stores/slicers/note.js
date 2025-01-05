import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import NotesAPI from "../../api/note";

export const fetchNotes = createAsyncThunk("notes/fetchNotes", async () => {
  const response = await NotesAPI.getAllNotes();
  return response;
});

export const addNoteAsync = createAsyncThunk(
  "notes/addNote",
  async (noteData, { dispatch }) => {
    const response = await NotesAPI.createNote(noteData);
    dispatch(fetchNotes());
    return response;
  }
);

export const updateNoteAsync = createAsyncThunk(
  "notes/updateNote",
  async ({ noteId, noteData }, { dispatch }) => {
    const response = await NotesAPI.updateNote(noteId, noteData);
    // Refetch notes after successful update
    dispatch(fetchNotes());
    return response;
  }
);

export const deleteNoteAsync = createAsyncThunk(
  "notes/deleteNote",
  async (noteId, { dispatch }) => {
    await NotesAPI.deleteNote(noteId);
    // Refetch notes after successful deletion
    dispatch(fetchNotes());
    return noteId;
  }
);

const notesSlice = createSlice({
  name: "notes",
  initialState: {
    notes: [],
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotes.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchNotes.fulfilled, (state, action) => {
        state.notes = action.payload;
        state.status = "succeeded";
      })
      .addCase(fetchNotes.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      });
  },
});

export default notesSlice.reducer;
