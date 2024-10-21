import 'dart:io' as io;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Plant Disease Detection',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  dynamic _image;
  final picker = ImagePicker();
  String _prediction = '';
  String? _apiResponseImage;
  double _confidence = 0.0;

  Future getImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);

    setState(() {
      if (pickedFile != null) {
        if (kIsWeb) {
          _image = pickedFile;
        } else {
          _image = io.File(pickedFile.path);
        }
        _prediction = '';
        _apiResponseImage = null;
      } else {
        print('No image selected.');
      }
    });

    if (_image != null) {
      await uploadImage(_image);
    }
  }

  Future<void> uploadImage(dynamic image) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://192.168.1.163:5000/predict'), 
    );

    if (kIsWeb) {
      request.files.add(
        http.MultipartFile.fromBytes(
          'image',
          await image.readAsBytes(),
          filename: 'image.jpg',
        ),
      );
    } else {
      request.files.add(
        await http.MultipartFile.fromPath('image', image.path),
      );
    }

    try {
      final response = await request.send();

      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final decodedData = json.decode(responseData);
        setState(() {
          _prediction = decodedData['prediction'];
          _confidence = decodedData['confidence'];
          _apiResponseImage = decodedData['image_url'];
        });
      } else {
        print('Error: ${response.reasonPhrase}');
      }
    } catch (e) {
      print('Error in uploadImage: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Plant Disease Detection'),
      ),
      body: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                if (_image == null)
                  Text('No image selected.')
                else if (kIsWeb)
                  Container(
                    width: MediaQuery.of(context).size.width * 0.8,
                    height: MediaQuery.of(context).size.height * 0.5,
                    child: Image.network(
                      _image.path,
                      fit: BoxFit.contain,
                    ),
                  )
                else
                  Container(
                    width: MediaQuery.of(context).size.width * 0.8,
                    height: MediaQuery.of(context).size.height * 0.5,
                    child: Image.file(
                      _image,
                      fit: BoxFit.contain,
                    ),
                  ),
                SizedBox(height: 20),
                if (_prediction.isNotEmpty)
                  Column(
                    children: [
                      Text(
                          'Prediction: $_prediction (Confidence: ${(_confidence * 100).toStringAsFixed(2)}%)'),
                      SizedBox(height: 10),
                      if (_apiResponseImage == null)
                        Text('Waiting for server response...'),
                      if (_apiResponseImage != null)
                        Container(
                          width: MediaQuery.of(context).size.width * 0.8,
                          height: MediaQuery.of(context).size.height * 0.5,
                          child: Image.network(
                            _apiResponseImage!,
                            fit: BoxFit.contain,
                          ),
                        ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
      
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: () => getImage(ImageSource.camera),
            tooltip: 'Take Photo',
            child: Icon(Icons.camera),
          ),
          SizedBox(height: 10),
          FloatingActionButton(
            onPressed: () => getImage(ImageSource.gallery),
            tooltip: 'Upload Image',
            child: Icon(Icons.photo_library),
          ),
        ],
      ),
    );
  }
}
