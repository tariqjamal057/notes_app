import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  fetchNotes,
  addNoteAsync,
  updateNoteAsync,
  deleteNoteAsync,
} from "../stores/slicers/note";
import Card from "../components/Card";
import Form from "../components/Form";

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentNote, setCurrentNote] = useState(null);
  const { notes = [] } = useSelector((state) => state.notes);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchNotes());
  }, [dispatch]);

  const handleEdit = (note) => {
    setCurrentNote(note);
    setIsModalOpen(true);
  };

  const handleDelete = (noteId) => {
    dispatch(deleteNoteAsync(noteId));
  };

  const handleSave = (note) => {
    if (currentNote) {
      dispatch(updateNoteAsync({ noteId: currentNote.id, noteData: note }));
    } else {
      dispatch(addNoteAsync(note));
    }
    setIsModalOpen(false);
  };

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h2 className="text-2xl font-bold">Your Notes</h2>
        <button
          onClick={() => {
            setCurrentNote(null);
            setIsModalOpen(true);
          }}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add Note
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.isArray(notes) &&
          notes.map((note) => (
            <Card
              key={note.id}
              note={note}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
      </div>
      <Form
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSave}
        note={currentNote}
      />
    </div>
  );
};

export default Home;
