import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { NavItem } from "react-bootstrap";

export default function Sidebar() {
  return (
    <Nav className="flex-column Sidebar">
      <Nav.Item>
        <Nav.Link href="/">Feed</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link href="/explore">Explore</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link href="/liked">Liked</Nav.Link>
      </Nav.Item>
    </Nav>
  );
}