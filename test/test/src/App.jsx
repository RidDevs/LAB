
import List from'./list';
import Home from './pages/home';
import About from './pages/about';
import {Routes,Route,BrowserRouter,Link} from 'react-router-dom';
function App() {
  const users=[
        {id:1,name:"a"},
        {id:2,name:"b"},
        {id:3,name:"c"}
    ];

  return (
    <BrowserRouter>
      <h2>USER LIST</h2>
      <List users={users}/>

      <nav>

        <Link to='/'>Home</Link>
         <Link to='/about'>About</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home></Home>}></Route>
        <Route path="/about" element={<About></About>}></Route>
      </Routes>
      

    </BrowserRouter>
  );
}

export default App;
