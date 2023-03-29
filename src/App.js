import Container from 'react-bootstrap/Container';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import ApiProvider from './contexts/ApiProvider';
import Header from './components/Header';
import FeedPage from './pages/FeedPage';
import ExplorePage from './pages/ExplorePage';
import PrompterPage from './pages/PrompterPage';
import LikedPage from './pages/LikedPage';
import LoginPage from './pages/LoginPage';

function App() {
  return (
    <Container fluid className="App">
      <BrowserRouter>
        <ApiProvider>
          <Header />
          <Routes>
            <Route path="/" element={<FeedPage />} />
            <Route path="/explore" element={<ExplorePage />} />
            <Route path="/prompter/:id" element={<PrompterPage />} />
            <Route path="/liked" element={<LikedPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </ApiProvider>
      </BrowserRouter>
    </Container>
  );
}

export default App;
