import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

const Form = ({ isOpen, onClose, onSubmit, note }) => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // Use useEffect to update state when note prop changes
  useEffect(() => {
    if (note) {
      setTitle(note.title || "");
      setContent(note.content || "");
    } else {
      // Reset form when creating a new note
      setTitle("");
      setContent("");
    }
  }, [note]);

  const handleSubmit = () => {
    onSubmit({
      id: note?.id,
      title,
      content,
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <motion.div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="bg-white rounded-lg shadow-lg p-6 w-96">
        <h2 className="text-lg font-bold mb-4">
          {note ? "Edit Note" : "Add Note"}
        </h2>
        <input
          type="text"
          placeholder="Title"
          className="w-full border rounded px-3 py-2 mb-4"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <ReactQuill value={content} onChange={setContent} className="mb-4" />
        <div className="flex justify-end space-x-4">
          <button
            onClick={onClose}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Save
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default Form;
