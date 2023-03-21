import React from "react";
import "./playergrid.css";

const PlayerGrid = ({ players }) => {
  return (
    <div className="player-grid">
      {players.map((player, index) => (
        <div className="player" key={index}>
          {player.name}
        </div>
      ))}
    </div>
  );
};

export default PlayerGrid;
