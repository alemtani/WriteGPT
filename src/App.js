function App() {
  const works = [
    {
      id: '1',
      title: 'Hello, world!',
      genre: 'fiction',
      body: 'This is a test work',
      timestamp: 'a minute ago',
      prompter: {
        username: 'susan',
      },
    },
    {
      id: '2',
      title: 'Second work',
      genre: 'nonfiction',
      body: 'This is a second test work',
      timestamp: 'an hour ago',
      prompter: {
        username: 'john',
      },
    },
  ];

  return (
    <>
      <h1>WriteGPT</h1>
      {works.length === 0 ?
        <p>There are no works to display.</p>
      :
        works.map(work => {
          return (
            <p key={work.id}>
              <b>{work.title}</b>
              <br />
              A work of {work.genre} prompted {work.timestamp} by <i>{work.prompter.username}</i>
              <br />
              {work.body}
            </p>
          );
        })
      }
    </>
  );
}

export default App;
