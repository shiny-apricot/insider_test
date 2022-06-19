import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Table from "./Table";
import './scss/table.scss';

function App() {
  // get team_table as json,
  // the json include "team_name", "played", "won", "drown", "lost", "GF", "GA", "GD", "points"
  const [team_table, setTeamTable] = useState({
    teams: [],
  });
  const [league_matches, setLeagueMatches] = useState({
    matches: [],
  });

  const [is_done, setIsDone] = useState(false);

  useEffect(() => {
    fetch("/table").then((res) =>
    res.json().then((team_table) => {
        // Setting a data from api
        setTeamTable({
            teams: team_table.teams,
        });
    })
  );
  }
  , []);

  // async fetch_table function
  const fetch_table = async () => {
    const response = await fetch("/table");
    const data = await response.json();
    setTeamTable({
      teams: data.teams,
    });
  }

  console.log("team_table: ", team_table);

  var week_number = 4;
  // create a string var as "week match result"
  var week = "Week " + week_number;

  const standing_columns = React.useMemo(() => [
    {
      Header: "League Table",
      columns: [
        {
          Header: "Team",
          accessor: "team_name",
        },
        {
          Header: "P",
          accessor: "played",
        },
        {
          Header: "W",
          accessor: "won",
        },
        {
          Header: "D",
          accessor: "drown",
        },
        {
          Header: "L",
          accessor: "lost",
        },
        {
          Header: "GF",
          accessor: "GF",
        },
        {
          Header: "GA",
          accessor: "GA",
        },
        {
          Header: "GD",
          accessor: "GD",
        },
        {
          Header: "Pts",
          accessor: "points",
        },
      ]
    }    
  ], []);

  const matches_columns = React.useMemo(() => [
    {
      Header: "Match Results",
      columns: [
          {
            Header: "Home",
            accessor: "home",
          },
          {
            Header: "Score",
            accessor: "score",
          },
          {
            Header: "Away",
            accessor: "away",
          },
      ]
    }
  ], []);

  const prediction_columns = React.useMemo(() => [
    {
      Header: "Prediction",
      accessor: "predictions"
    }
  ], []);

  // POST request to '/generate_league' endpoint asynchronously

  const generate_league = async () => {
    setIsDone(false);
    const response = await fetch("/generate_league", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    });
    const data = await response.json();
    setTeamTable({
      teams: data.teams,
    });
  }

  const check_is_done = async () => {
    const final_response = await fetch("/is_done",{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    const is_done_res = await final_response.json();

    console.log("is_done_res: ", is_done_res);
    if(is_done_res){
      setIsDone(true);
    }
    else{
      setIsDone(false);
    }
  }


  const next_week = async () => {
    check_is_done();
    const response = await fetch("/next_week", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log("data: ", data);
    setLeagueMatches({
      matches: data,
    });
    fetch_table();
  }


  const play_all = async () => {
    const response = await fetch("/play_all", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    fetch_table();
  }

  const championship_board = () => {
    console.log("is_done: ", is_done);
    if( is_done ){
      console.log("championship_board: ", team_table.teams[0].team_name);
      return (
        <div class="championship-banner">
          <h2>CHAMPION {team_table.teams[0].team_name}</h2>
        </div>
      );
    }
    else{
      // return invisible div
      return (
        <div>
        </div>
      );
    }
  }
  // user should select team_count to fetch numbers teams
  // it start from 1 to 20
  
  // display team_table as table with "played", "won", "drown", "lost", "GF", "GA", "GD", "points"
  // add two button as "play all", align it to left and "next week" to right
  // when click "play all", display all match result
  // when click "next week", go one week forward
  return (
      <div className="App" >
        <button type="button" class="btn btn-top btn-primary btn-lg btn-block" onClick={generate_league}>
          Create a Random League
        </button>
        {championship_board()}
        <div class="table-wrapper">
          <Table columns={standing_columns} data={team_table.teams} />
          <div class="second-table-wrapper">
            <Table columns={matches_columns} data={league_matches.matches} />
            {/* <Table columns={prediction_columns} data={league_matches.matches} /> */}
          </div>
          <button id="playall" class="btn btn-primary btn-lg btn-block f-l" type="button" onClick={play_all}>
              Play All
          </button>
          <button id="nextweek" class="btn btn-primary btn-lg btn-block f-r" type="button" onClick={next_week}>
              Next Week
          </button>
        </div>
      </div>
  );
}

export default App;