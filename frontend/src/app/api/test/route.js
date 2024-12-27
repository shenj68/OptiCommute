// app/api/upload/route.js

export async function GET(request) {
  return {
    status: 200,
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ message: "Hello world" }),
  };
}

export async function POST(request) {
  return {
    status: 200,
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ message: "Hello world" }),
  };
}
