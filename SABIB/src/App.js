import './App.css';
import Header from './components/UI/Header/Header';
import Sections from './components/sections/Sections';
import Footer from './components/UI/Footer/Footer';


function App() {
  return (
    <><div className="App">
      <Header />
      <main>
        <Sections />
      </main>
      <Footer />
    </div>
    </>
  );
}

export default App;
