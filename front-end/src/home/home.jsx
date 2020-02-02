import React from 'react';
import { Timeline, Menu, History } from '@material-ui/icons';
import {
  Container,
  Drawer,
  List,
  ListItem,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  ListItemIcon,
  ListItemText,
  Paper,
} from '@material-ui/core';
import { css } from 'emotion';
import {
  XYPlot,
  LineSeries,
  VerticalGridLines,
  HorizontalGridLines,
  XAxis,
  YAxis,
} from 'react-vis';
import '../../node_modules/react-vis/dist/style.css';

class Home extends React.Component {
  state = {
    open: false,
    showChart: true,
    showHistory: false,
  };
  render() {
    const data = [
      { x: 0, y: 8 },
      { x: 1, y: 5 },
      { x: 2, y: 4 },
      { x: 3, y: 9 },
      { x: 4, y: 1 },
      { x: 5, y: 7 },
      { x: 6, y: 6 },
      { x: 7, y: 3 },
      { x: 8, y: 2 },
      { x: 9, y: 0 },
    ];
    const history = [
      { question: 'How are you ?', answer: 'good and you?' },
      { question: "I'm fine but I'm feeling a bit blue", answer: 'why are you blue?' },
      { question: 'not blue, i feel sad.', answer: 'oh sorry about that' },
    ];
    return (
      <>
        <AppBar position="static">
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu" onClick={this.toggleDrawer}>
              <Menu />
            </IconButton>
            <Typography variant="h6">Ms. Rogers Dashboard</Typography>
          </Toolbar>
        </AppBar>
        <div className={css({ display: this.state.showChart ? '' : 'none' })}>
          <Box display="flex" justifyContent="center" mt={1} mb={1}>
            <XYPlot height={window.innerHeight * 0.9} width={window.innerWidth * 0.9}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />
              <LineSeries data={data} />
            </XYPlot>
          </Box>
        </div>
        <div className={css({ display: this.state.showHistory ? '' : 'none' })}>
          <Container maxWidth="md">
            {history.map(item => (
              <Box mt={1} mb={1}>
                <Paper>
                  <Typography>{item.question}</Typography>
                  <Typography>{item.answer}</Typography>
                </Paper>
              </Box>
            ))}
          </Container>
        </div>
        <div>
          <Drawer open={this.state.open} onClose={this.closeDrawer}>
            <List className={css({ marginTop: 100 })}>
              <ListItem
                onClick={() => {
                  this.setState({ showChart: true, showHistory: false });
                }}
              >
                <ListItemIcon>
                  <Timeline />
                </ListItemIcon>
                <ListItemText primary={'Sentiment Progression'} />
              </ListItem>
              <ListItem
                onClick={() => {
                  this.setState({ showChart: false, showHistory: true });
                }}
              >
                <ListItemIcon>
                  <History />
                </ListItemIcon>
                <ListItemText primary={'Conversation History'} />
              </ListItem>
            </List>
          </Drawer>
        </div>
      </>
    );
  }
  toggleDrawer = () => {
    this.setState({
      open: true,
    });
  };

  closeDrawer = () => {
    this.setState({
      open: false,
    });
  };
}

export default Home;
