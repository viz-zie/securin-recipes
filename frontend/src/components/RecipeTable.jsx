import React, { useEffect, useState } from "react";
import axios from "axios";
import RecipeDrawer from "./RecipeDrawer";

const RecipeTable = () => {
  const [recipes, setRecipes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [page, setPage] = useState(1);

  const fetchRecipes = async () => {
    const res = await axios.get(`http://localhost:5000/api/recipes?page=${page}&limit=10`);
    setRecipes(res.data.data);
  };

  useEffect(() => { fetchRecipes(); }, [page]);

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Cuisine</th>
            <th>Rating</th>
            <th>Total Time</th>
            <th>Serves</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map((r, i) => (
            <tr key={i} onClick={() => setSelected(r)}>
              <td>{r.title}</td>
              <td>{r.cuisine}</td>
              <td>{r.rating} ★</td>
              <td>{r.total_time} mins</td>
              <td>{r.serves}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div>
        <button className="button" onClick={() => setPage(page - 1)} disabled={page === 1}>
          Prev
        </button>
        <span> Page {page} </span>
        <button className="button" onClick={() => setPage(page + 1)}>
          Next
        </button>
      </div>

      {selected && <RecipeDrawer recipe={selected} onClose={() => setSelected(null)} />}
    </div>
  );
};

export default RecipeTable;
