import React from 'react';
import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [categories, setCategories] = useState(null);
  useEffect(() => {
    async function getCategories() {
      const res = await fetch('/api/categories');
      const categories = await res.text();
      setCategories(categories);
    }
    getCategories();
  }, []);
  return (
    <main>
      <h1>Create React App + Python API</h1>
      <h2>
        Deployed with{' '}
        <a
          href="https://vercel.com/docs"
          target="_blank"
          rel="noreferrer noopener"
        >
          Vercel
        </a>
        !
      </h2>
      <p>
        <a
          href="https://github.com/vercel/vercel/tree/master/examples/create-react-app"
          target="_blank"
          rel="noreferrer noopener"
        >
          This project
        </a>{' '}
        was bootstrapped with{' '}
        <a href="https://facebook.github.io/create-react-app/">
          Create React App
        </a>{' '}
        and contains three directories, <code>/public</code> for static assets,{' '}
        <code>/src</code> for components and content, and <code>/api</code>{' '}
        which contains a serverless <a href="https://golang.org/">Go</a>{' '}
        function. See{' '}
        <a href="/api/categories">
          <code>api/categories</code> for the Categories API with Python
        </a>
        .
      </p>
      <br />
      <h2>All Categories:</h2>
      <p>{categories ? categories : 'Loading categories...'}</p>
    </main>
  );
}

export default App;
