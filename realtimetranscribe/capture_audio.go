package main

import (
	"fmt"
	"log"
	"os/exec"
	"time"

	"github.com/gordonklaus/portaudio"
)

const (
	sampleRate    = 44100 // CD-quality audio
	channels      = 1     // Mono audio
	framesPerSec  = 4410  // Buffer size (1 second)
	bitsPerSample = 16    // 16-bit PCM
)

func main() {
	// Initialize PortAudio
	err := portaudio.Initialize()
	if err != nil {
		log.Fatalf("Error initializing PortAudio: %v", err)
	}
	defer portaudio.Terminate()

	// Create an input stream
	buffer := make([]int16, framesPerSec)
	stream, err := portaudio.OpenDefaultStream(1, 0, sampleRate, len(buffer), buffer)
	if err != nil {
		log.Fatalf("Error opening audio stream: %v", err)
	}
	defer stream.Close()

	// Start recording
	err = stream.Start()
	if err != nil {
		log.Fatalf("Error starting audio stream: %v", err)
	}

	fmt.Println("Recording... Press Ctrl+C to stop.")

	for i := 0; i < 5; i++ { // Record for 5 seconds (change as needed)
		// Capture 1 second of audio
		err = stream.Read()
		if err != nil {
			log.Fatalf("Error reading audio: %v", err)
		}

		fmt.Println(buffer)

		// Save as a new audio file via FFmpeg
		filename := fmt.Sprintf("output_%d.mp3", i)
		err = saveWithFFmpeg(filename, buffer)
		if err != nil {
			log.Fatalf("Error encoding with FFmpeg: %v", err)
		}

		fmt.Println("Saved:", filename)
		time.Sleep(time.Second) // Wait 1 second before capturing again
	}

	// Stop the stream
	err = stream.Stop()
	if err != nil {
		log.Fatalf("Error stopping stream: %v", err)
	}

	fmt.Println("Recording stopped.")
}

// saveWithFFmpeg writes raw PCM data to FFmpeg and saves it as MP3
func saveWithFFmpeg(filename string, buffer []int16) error {
	// Create FFmpeg command to encode raw PCM to MP3
	cmd := exec.Command("ffmpeg",
		"-f", "s16le", // PCM 16-bit little-endian
		"-ar", "44100", // Sample rate
		"-ac", "1", // Mono
		"-i", "pipe:0", // Read from stdin
		"-b:a", "192k", // Set bitrate (192kbps MP3)
		filename, // Output file
	)

	// Get stdin pipe for writing PCM data
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return err
	}

	// Start FFmpeg process
	err = cmd.Start()
	if err != nil {
		return err
	}

	// Write raw PCM data to FFmpeg's stdin
	for _, sample := range buffer {
		_, err := stdin.Write([]byte{byte(sample & 0xFF), byte(sample >> 8)}) // Little-endian format
		if err != nil {
			return err
		}
	}

	// Close stdin to signal FFmpeg that input is complete
	err = stdin.Close()
	if err != nil {
		return err
	}

	// Wait for FFmpeg to finish
	err = cmd.Wait()
	if err != nil {
		return err
	}

	return nil
}
