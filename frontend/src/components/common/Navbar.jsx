import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <NavLink to="/">
        Home
      </NavLink>

      <NavLink to="/planner">
        Trip Planner
      </NavLink>
    </nav>
  );
}

export default Navbar;