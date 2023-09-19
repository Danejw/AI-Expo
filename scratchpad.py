RESPONSE_FORMAT_WITH_COMMAND = """```ts
interface Response {
    thoughts: {
        // Thoughts
        text: string;
        reasoning: string;
        // Short markdown-style bullet list that conveys the long-term plan
        plan: string;
        // Constructive self-criticism
        criticism: string;
        // Summary of thoughts to say to the user
        speak: string;
    };
    command: {
         name: string;
         args: Record<string, any>;
     };
}
```"""

DEFAULT_TRIGGERING_PROMPT = (
    "Determine exactly one command to use based on the given goals "
    "and the progress you have made so far, "
    "and respond using the JSON schema specified previously:"
)


{
  "story": "[Complete Story Generated Previously]",
  "instructions": {
    "reasoning": {
      "identifyThemes": "Identify the core themes and emotions of the story.",
      "determineGenre": "Determine the game genre that best suits the narrative.",
      "keyGameplayEvents": "Reflect on key moments in the story that can serve as main gameplay events or turning points."
    },
    "plan": {
      "gameMechanics": "Outline the game's main mechanics and align them with the story's themes.",
      "worldDesign": "Describe the game world's design considering locations, assets, and ambiance.",
      "playerProgression": "Detail the player's progression in the game.",
      "additionalElements": "Define additional gameplay elements like side-quests or mini-games."
    },
    "criticism": {
      "potentialChallenges": "Identify potential challenges in adapting the story to a game format.",
      "narrativeAdjustments": "Consider areas where the narrative might need adjustments for gameplay mechanics or pacing.",
      "ethicalConsiderations": "Reflect on ethical or moral considerations when portraying certain story elements."
    },
    "output": "Compile these insights into a cohesive technical document outlining the game elements."
  }
}
