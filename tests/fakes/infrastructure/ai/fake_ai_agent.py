class FakeAIAgent:
  async def send_content(self, prompt: str, system_prompt: str) -> str:
    return """
{
  "ts": [{
    "t": "Topic 1",
    "st": [{
      "t": "Subtopic 1-1",
      "sm": ["Book 1", "Video 1", "Book 2", "Book 3"]
    }, {
      "t": "Subtopic 1-2",
      "sm": ["Book 1", "Book 3"]
    }, {
      "t": "Subtopic 1-3",
      "sm": [ "Book 2", "Book 4"]
    }],
    "qs": [{
      "t": "Question 1",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "a"
    }, {
      "t": "Question 2",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "b"
    }, {
      "t": "Question 3",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "d"
    }]
  }, {
    "t": "Topic 2",
    "st": [{
      "t": "Subtopic 2-1",
      "sm": ["Book 1"]
    }, {
      "t": "Subtopic 2-2",
      "sm": ["Book 3", "Book 5"]
    }, {
      "t": "Subtopic 2-3",
      "sm": [ "Book 4", "Book 6"]
    }],
    "qs": [{
      "t": "Question 1",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "b"
    }, {
      "t": "Question 2",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "c"
    }, {
      "t": "Question 3",
      "os": [{
        "t": "Option 1",
        "o": "a"
      }, {
        "t": "Option 2",
        "o": "b"
      }, {
        "t": "Option 3",
        "o": "c"
      }, {
        "t": "Option 4",
        "o": "d"
      }],
      "a": "d"
    }]
  }]
}
"""
