INSERT INTO users (email, password_hash, created_at)
VALUES (
  'user@example.com', 
  '$2b$12$S7vBdW3sQlU5kzqkE9QY.9mZJ7r8fz1JcXoLp5d5nYvL1aXkZ8XbC',
  NOW()
);