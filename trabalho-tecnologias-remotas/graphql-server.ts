// graphql-server.ts
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { users, songs, playlists, getPlaylistsByUser, getSongsByPlaylist, User, Playlist } from './data';

// Schema Definition
const typeDefs = `#graphql
  type Song {
    id: Int
    title: String
    artist: String
  }

  type Playlist {
    id: Int
    name: String
    user_id: Int
    song_ids: [Int]
    songs: [Song] # Campo calculado (Resolver)
  }

  type User {
    id: Int
    name: String
    email: String
    playlists: [Playlist] # Campo calculado (Resolver)
  }

  type Query {
    users: [User]
    songs: [Song]
    user(id: Int!): User
  }
`;

// Resolvers
const resolvers = {
    Query: {
        users: () => users,
        songs: () => songs,
        user: (_: any, args: { id: number }) => users.find(u => u.id === args.id),
    },
    User: {
        playlists: (parent: User) => getPlaylistsByUser(parent.id),
    },
    Playlist: {
        songs: (parent: Playlist) => getSongsByPlaylist(parent.id),
    },
};

const startServer = async () => {
    const server = new ApolloServer({
        typeDefs,
        resolvers,
    });

    const { url } = await startStandaloneServer(server, {
        listen: { port: 8002 },
    });

    console.log(`GraphQL Server running on ${url}`);
};

startServer();
