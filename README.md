# tiktok-video-generation

This repository contains the code for our Introduction to AI project. The project is about generating TikTok videos using a combination of different generative AI models.

## Getting started

To set up the project, follow these steps:

1. Clone the repository
2. Create a new Conda environement based on the documented dependencies `conda env create --file environment.yml`
3. Activate the Conda environment `conda activate cmuintroaiproject`

Add new dependencies using `conda install <package>` and update the `environment.yml` file using `conda env export --name cmuintroaiproject > environment.yml`.

4. Add environment variables to the `.env` file. You can use the `.env.example` file as a template.

## Running the project

To run the project, execute the following command:

```bash
python main.py
```

## Project Structure

The project is structured as follows:

```plaintext
.
├── Dockerfile                      # Dockerfile for the project
├── README.md                       # This file
├── .env                            # Environment variables
├── environment.yml                 # Conda environment file
├── main.py                         # Main file to run the project
└── services                        # Services for the project
    ├── scripting_service.py
    └── voice_generator_service.py
```


## Architecture

The video different components are generated step-by-step:

```mermaid
sequenceDiagram
    TikTokGenerator->>ScriptingServive: location
    ScriptingServive->>ScriptingServive: Generate script
    ScriptingServive->>TikTokGenerator: script

    TikTokGenerator->>PicturePromptGeneratorServuce: script, location
    PicturePromptGeneratorServuce->>PicturePromptGeneratorServuce: generate picture prompts
    PicturePromptGeneratorServuce->>TikTokGenerator: picture_prompt[]

    TikTokGenerator->>VoiceGeneratorService: script
    VoiceGeneratorService->>VoiceGeneratorService: Generate voice as mp3
    VoiceGeneratorService->>TikTokGenerator: voice

    TikTokGenerator->>PictureGenerationService: picture_prompt[]
    PictureGenerationService->>PictureGenerationService: Generate pictures
    PictureGenerationService->>TikTokGenerator: pictures[]

    TikTokGenerator->>PictureAnimationService: pictures[]
    PictureAnimationService->>PictureAnimationService: Apply Ken Burns effect
    PictureAnimationService->>TikTokGenerator: animated_pictures[]

    TikTokGenerator->>VideoGenerationService: script, voice, animated_pictures[]
    VideoGenerationService->>VideoGenerationService: Generate video
    VideoGenerationService->>TikTokGenerator: video
```


The TikTokGenerator (residing in a notebook) is thus the main orchestrator of the different services.:


```mermaid
    graph TD
        A[TikTokGenerator] -->|1. Generates script| B(ScriptingServive)
        A -->|2. Generates picture prompts| C(PicturePromptGeneratorServuce)
        A -->|3. Generates voice| D(VoiceGeneratorService)
        A -->|4. Generates pictures| E(PictureGenerationService)
        A -->|5. Animates pictures| F(PictureAnimationService)
        A -->|6. Generates video| G(VideoGenerationService)
        B --> B
        C --> C
        D --> D
        E --> E
        F --> F
        G --> G
```

The different services rely on some external components for which API-Keys need to be configured in the `.env` file:

```mermaid
    C4Component
    title Component diagram for TikTok-Video-Generation

    Component(main, "TikTokGenerator", "Notebook", "Main orchestrator of the different services")

    Container_Boundary(services, "TikTok-Video-Generation Services", "Services for generating TikTok videos") {
        Component(scripting, "ScriptingServive", "Python Script", "Generates a script for a video based on a location.")
        Component(picture_prompt, "PicturePromptGeneratorServuce", "Python Script", "Generates picture prompts based on a script and location.")
        Component(voice, "VoiceGeneratorService", "Python Script", "Generates a voice for a video based on a script.")
        Component(pictures, "PictureGenerationService", "Python Script", "Generates pictures based on picture prompts.")
        Component(animated_pictures, "PictureAnimationService", "Python Script", "Applies the Ken Burns effect to pictures.")
        Component(video, "VideoGenerationService", "Python Script", "Creates a video from a script (subtitles), voice, and animated pictures.")
    }

    System_Ext(ppl, "Perplexity API", "Provides text completion and generation services using RAG.")
    System_Ext(openai, "OpenAI API", "Provides semantic embeddings.")
    System_Ext(polly, "AWS Polly", "Generates voice from text input.")


    Rel(scripting, ppl, "Uses")
    Rel(picture_prompt, openai, "Uses")
    Rel(picture_prompt, ppl, "Uses")
    Rel(voice, polly, "Uses")

```