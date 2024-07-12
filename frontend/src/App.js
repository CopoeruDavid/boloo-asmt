import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PollComponent from './PollComponent';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

function App() {
  const [polls, setPolls] = useState([]);
  const [currentPoll, setCurrentPoll] = useState(null);
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchPolls();
  }, []);

  const fetchPolls = async () => {
    const response = await axios.get('http://192.168.0.113:8000/polls');
    setPolls(response.data);
  };

  const fetchPoll = async (id) => {
    const response = await axios.get(`http://192.168.0.113:8000/poll/${id}`);
    setCurrentPoll(response.data);
    fetchResults(id);
  };

  const fetchResults = async (id) => {
    const response = await axios.get(`http://192.168.0.113:8000/results/${id}`);
    setResults(response.data);
  };

  const submitVote = async (option) => {
    await axios.post('http://192.168.0.113:8000/vote', { 
      question_id: currentPoll.id, 
      option 
    });
    fetchResults(currentPoll.id);
  };

  const formatResultsForChart = (results) => {
    if (!results) return [];
    return Object.entries(results).map(([label, value], index) => ({
      id: index,
      value,
      label
    }));
  };

  if (polls.length === 0) return <div>Loading polls...</div>;

  return (
    <div>
      <h1>Polls</h1>
      {/* Itterates and shows all the polls that are available */}
      <Stack spacing={2} direction="row">
      {polls.map(poll => (
        <Button variant="contained" key={poll.id} onClick={() => fetchPoll(poll.id)}>
          {poll.question}
        </Button>
      ))}
      </Stack>

      {/* itterate through the options available for the specific poll */}
      {currentPoll && (
        <div>
          <h2>{currentPoll.question}</h2>
          <Stack spacing={2} direction="row">
          {currentPoll.options.map(option => (
            <Button variant="contained" key={option} onClick={() => submitVote(option)}>
              {option}
            </Button>
          ))}
          </Stack>
        </div>
      )}

      {/* Plots the results and shows them in a pie chart defined in PollComponent.js */}
      {results && (
        <div>
          <h2>Results:</h2>
          <PollComponent data={formatResultsForChart(results)} />
          {/* {Object.entries(results).map(([option, votes]) => (
            <p key={option}>{option}: {votes} votes</p>
          ))} */}
        </div>
      )}
    </div>
  );
}

export default App;