import React, { useState, useRef, useEffect } from 'react';
import { View, Image, Alert, TouchableOpacity, StyleSheet } from 'react-native';
import { CameraView } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';
import { Ionicons } from '@expo/vector-icons';

const CameraComponent = () => {
  const [image, setImage] = useState(null);
  const cameraRef = useRef(null);

  useEffect(() => {
    const requestPermissions = async () => {
      await MediaLibrary.requestPermissionsAsync();
      await expo-camera.requestCameraPermissionsAsync();
    };
    requestPermissions();
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const picture = await cameraRef.current.takePictureAsync();
        setImage(picture.uri);
      } catch (err) {
        console.log('Error while taking the picture:', err);
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const savePicture = async () => {
    if (image) {
      try {
        const asset = await MediaLibrary.createAssetAsync(image);
        Alert.alert('Receipt saved!');
        setImage(null);
        // Receipt processing goes logic here
      } catch (err) {
        console.log('Error while saving the picture:', err);
        Alert.alert('Error', 'Failed to save picture');
      }
    }
  };

  return (
    <View style={styles.container}>
      {!image ? (
        <>
          <CameraView
            style={styles.camera}
            ref={cameraRef}
          />
          <View style={styles.bottomControlsContainer}>
            <TouchableOpacity 
              style={styles.cameraButton} 
              onPress={takePicture}
            >
              <Ionicons name="camera" size={40} color="#fff" />
            </TouchableOpacity>
          </View>
        </>
      ) : (
        <>
          <Image source={{ uri: image }} style={styles.camera} />
          <View style={styles.bottomControlsContainer}>
            <TouchableOpacity 
              style={styles.controlButton} 
              onPress={() => setImage(null)}
            >
              <Ionicons name="close" size={30} color="#fff" />
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.controlButton} 
              onPress={savePicture}
            >
              <Ionicons name="checkmark" size={30} color="#fff" />
            </TouchableOpacity>
          </View>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  camera: {
    flex: 1,
    width: '100%',
  },
  bottomControlsContainer: {
    height: 150,
    backgroundColor: 'black',
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  cameraButton: {
    backgroundColor: '#007AFF',
    width: 70,
    height: 70,
    borderRadius: 35,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  controlButton: {
    backgroundColor: '#007AFF',
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 20,
  },
});

export default CameraComponent;