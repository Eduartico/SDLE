import BottomAppBar from "../components/BottomAppBar";

const Recipes = () => {
  return (
    <div>
      <div className="bottom-app-bar">Recipes</div>
      <div
        style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          width: "100%",
          background: "#f0f0f0",
          padding: "10px",
        }}
      >
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Recipes;
