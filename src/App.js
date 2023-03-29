import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import Body from './components/Body';
import Works from './components/Works';

function App() {
  return (
    <Container fluid className="App">
      <Header />
      <Body sidebar>
        <Works />
      </Body>
    </Container>
  );
}

export default App;
