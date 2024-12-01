import React, { useState } from 'react';
import { Modal, View, Text, TouchableOpacity, TouchableWithoutFeedback, Alert,StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as MediaLibrary from 'expo-media-library';

const ActionButtonWithModal = ({ navigation }) => {
  const [modalVisible, setModalVisible] = useState(false);

  const handleCameraPress = () => {
    setModalVisible(false);
    navigation.navigate('Camera');
  };

  const handleGalleryPress = async () => {
    const { status } = await MediaLibrary.requestPermissionsAsync();
    if (status === 'granted') {
      try {
        const asset = await MediaLibrary.getAssetsAsync({
          mediaType: 'photo',
          first: 1,
        });
        setModalVisible(false);
        Alert.alert('Success', 'Gallery image selected!');
      } catch (error) {
        Alert.alert('Error', 'Failed to access gallery');
      }
    } else {
      Alert.alert('Permission required', 'Please allow access to your photos');
    }
  };

  const handleManualPress = () => {
    setModalVisible(false);
    navigation.navigate('Input');
  };
  

  return (
    <>
      <TouchableOpacity
        style={styles.actionButton}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="chevron-up-outline" size={30} color="#fff" />
      </TouchableOpacity>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <TouchableWithoutFeedback onPress={() => setModalVisible(false)}>
          <View style={styles.modalOverlay}>
            <TouchableWithoutFeedback>
              <View style={styles.modalContent}>
                <ModalOption
                  icon="camera"
                  text="Take Photo"
                  onPress={handleCameraPress}
                />
                <ModalOption
                  icon="images"
                  text="Choose from Gallery"
                  onPress={handleGalleryPress}
                />
                <ModalOption
                  icon="create"
                  text="Manual Input"
                  onPress={handleManualPress}
                />
              </View>
            </TouchableWithoutFeedback>
          </View>
        </TouchableWithoutFeedback>
      </Modal>
    </>
  );
};

// Helper component to reduce repetition
const ModalOption = ({ icon, text, onPress }) => (
  <TouchableOpacity style={styles.modalOption} onPress={onPress}>
    <Ionicons name={icon} size={24} color="#333" />
    <Text style={styles.modalOptionText}>{text}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  actionButton: {
    position: 'absolute',
    bottom: 30,
    right: 30,
    backgroundColor: '#007AFF',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  modalOption: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  modalOptionText: {
    fontSize: 16,
    marginLeft: 15,
    color: '#333',
  },
});

export default ActionButtonWithModal;