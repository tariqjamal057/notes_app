import React from "react";
import { motion } from "framer-motion";

const Card = ({ note, onEdit, onDelete }) => {
  return (
    <motion.div
      className="w-full bg-white shadow-md rounded-lg p-3 flex flex-col justify-between"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div>
        <h3 className="text-xl font-semibold mb-2">{note.title}</h3>
        <div
          className="text-gray-600 mb-4"
          dangerouslySetInnerHTML={{ __html: note.content }}
        />
      </div>
      <div className="mt-4 flex space-x-4">
        <button
          onClick={() => onEdit(note)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(note.id)}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </motion.div>
  );
};

export default Card;
