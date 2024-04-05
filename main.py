import services.scripting_service as scripting_service
import services.voice_generator_service as voice_generator_service
import services.video_editing_service as video_editing_service

def main():
    print("Welcome to Tik-Tok Travel Video Generator")
    print("Please enter a location for travel information:")
    location = input()
    
    message_content = scripting_service.get_travel_information(location)
    voice_content = voice_generator_service.synthesize_speech(message_content)

    # need finished audio and video files
    # edited_video = video_editing_service.run(audio, video)
    print("Finished Editing your Tik-Tok Travel Video!")



if __name__ == "__main__":
    main()
