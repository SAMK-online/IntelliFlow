import React, { useEffect, useRef } from 'react';
import { Box, Typography } from '@mui/material';
import { Network } from 'vis-network/standalone';
import { DataSet } from 'vis-data/standalone';
import { Node, Edge, Options } from 'vis-network/standalone';

export interface TopicsNetworkProps {
  data: string[];
  title?: string;
}

const TopicsNetwork: React.FC<TopicsNetworkProps> = ({ data, title }) => {
  const networkContainer = useRef<HTMLDivElement>(null);
  const networkInstance = useRef<Network | null>(null);

  useEffect(() => {
    if (!networkContainer.current || !data.length) return;

    // Create nodes from topics
    const nodes = new DataSet<Node>(
      data.map((topic, index) => ({
        id: index,
        label: topic,
        shape: 'box',
        color: {
          background: '#e3f2fd',
          border: '#2196f3',
          highlight: {
            background: '#2196f3',
            border: '#1976d2'
          }
        },
        font: { color: '#000' }
      }))
    );

    // Create edges between related nodes
    const edges = new DataSet<Edge>(
      data.flatMap((_, index) => {
        const connections: Edge[] = [];
        // Create connections between nodes based on proximity in the array
        // This is a simple example - you might want to use actual relationship data
        if (index < data.length - 1) {
          connections.push({
            id: `${index}-${index + 1}`,
            from: index,
            to: index + 1,
            arrows: {
              to: { enabled: true, scaleFactor: 0.5 }
            },
            color: { color: '#2196f3', opacity: 0.6 }
          });
        }
        return connections;
      })
    );

    // Configure network options
    const options: Options = {
      nodes: {
        shape: 'box',
        margin: { top: 10, right: 10, bottom: 10, left: 10 },
        borderWidth: 1,
        shadow: true
      },
      edges: {
        width: 1,
        smooth: {
          enabled: true,
          type: 'continuous',
          roundness: 0.5
        }
      },
      physics: {
        stabilization: true,
        barnesHut: {
          gravitationalConstant: -2000,
          springConstant: 0.04
        }
      },
      interaction: {
        hover: true,
        navigationButtons: true,
        keyboard: true
      }
    };

    // Create network
    const networkData = {
      nodes: nodes,
      edges: edges
    };
    
    networkInstance.current = new Network(
      networkContainer.current,
      networkData,
      options as Options
    );

    return () => {
      if (networkInstance.current) {
        networkInstance.current.destroy();
      }
    };
  }, [data]);

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {title && (
        <Typography variant="h6" gutterBottom align="center">
          {title}
        </Typography>
      )}
      <Box
        ref={networkContainer}
        sx={{
          flex: 1,
          border: '1px solid #e0e0e0',
          borderRadius: 1,
          bgcolor: '#fff'
        }}
      />
    </Box>
  );
};

export default TopicsNetwork;
