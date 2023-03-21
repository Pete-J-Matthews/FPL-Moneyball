import { useState } from "react";
import { AppBar, Tabs, Tab, Box, Container, Typography } from "@mui/material";
import { useMediaQuery } from "@mui/material";
import "./App.css";
import PlayerGrid from "./playergrid/playergrid";

const players = [
  { name: "Goalkeeper 1" },
  { name: "Goalkeeper 2" },
  { name: "Defender 1" },
  { name: "Defender 2" },
  { name: "Defender 3" },
  { name: "Defender 4" },
  { name: "Defender 5" },
  { name: "Midfielder 1" },
  { name: "Midfielder 2" },
  { name: "Midfielder 3" },
  { name: "Midfielder 4" },
  { name: "Midfielder 5" },
  { name: "Forward 1" },
  { name: "Forward 2" },
  { name: "Forward 3" },
];


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 2 }}>
          <Container>{children}</Container>
        </Box>
      )}
    </div>
  );
}

function App() {
  const [value, setValue] = useState(0);
  const handleChange = (event, newValue) => setValue(newValue);
  const isSmallScreen = useMediaQuery("(max-width: 600px)");

  return (
    <div className="App">
      <AppBar position="static">
        <Typography variant="h4" align="center" sx={{ flexGrow: 1 }}>
          FPL Moneyball
        </Typography>
      </AppBar>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab label="My Team" />
        <Tab label="Captain" />
        <Tab label="Team Selection" />
        <Tab label="Transfers" />
      </Tabs>
      <TabPanel value={value} index={0}>
        <PlayerGrid players={players} />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <PlayerGrid players={players} />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <PlayerGrid players={players} />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <PlayerGrid players={players} />
      </TabPanel>
    </div>
  );
}




export default App;
