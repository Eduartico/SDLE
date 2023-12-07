import BottomAppBar from "../components/BottomAppBar";

const Recipes = () => {
  return (
    <div>
      <div className="bottom-app-bar">
        This page is working, just empty for now
      </div>
      <div className="position-fixed bottom-0 start-0 w-100">
        <BottomAppBar />
      </div>
    </div>
  );
};

export default Recipes;
