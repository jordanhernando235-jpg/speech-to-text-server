import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:ffmpeg_kit_flutter_min_gpl/ffmpeg_kit.dart';
import 'package:path_provider/path_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String status = "No MP3 selected";

  Future<void> pickMp3() async {
    FilePickerResult? result =
    await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3'],
    );

    if (result == null) return;

    File mp3File = File(result.files.single.path!);

    setState(() {
      status = "Converting MP3...";
    });

    Directory tempDir = await getTemporaryDirectory();

    String wavPath = "${tempDir.path}/audio.wav";

    await FFmpegKit.execute(
      '-i "${mp3File.path}" -ar 16000 -ac 1 "$wavPath"',
    );

    setState(() {
      status = "WAV created:\\n$wavPath";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Speech To Text"),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: pickMp3,
                child: const Text("Upload MP3"),
              ),
              const SizedBox(height: 20),
              Text(
                status,
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}