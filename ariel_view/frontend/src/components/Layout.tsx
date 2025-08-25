import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container, CssBaseline } from '@mui/material';
import { styled } from '@mui/material/styles';

const MainContent = styled('main')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  marginTop: '64px',
  minHeight: 'calc(100vh - 64px)',
  backgroundColor: '#f5f5f5'
}));

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Ariel View
          </Typography>
        </Toolbar>
      </AppBar>
      <MainContent>
        <Container maxWidth="xl">
          {children}
        </Container>
      </MainContent>
    </Box>
  );
};
