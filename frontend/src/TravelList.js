import React, { useEffect, useState } from "react";
import axios from "axios";

const TravelList = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/db-test")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the data!", error);
      });
  }, []);

  return (
    <div>
      <h1>Travel Data</h1>
      {data ? (
        <div>
          <h2>{data.message}</h2>
          <pre>{JSON.stringify(data.data, null, 2)}</pre>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default TravelList;
