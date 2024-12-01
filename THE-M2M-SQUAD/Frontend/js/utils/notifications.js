import Toastify from 'toastify-js';
import Swal from 'sweetalert2';
import 'toastify-js/src/toastify.css';

export const showToast = (message, type = 'info') => {
    const iconMap = {
        success: '✔️',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    Toastify({
        text: `<div class="icon">${iconMap[type]}</div><div>${message}</div>`,
        duration: 3000,
        gravity: 'bottom', // 'top' or 'bottom'
        position: 'left', // 'left', 'center' or 'right'
        className: `toastify ${type}`,
        stopOnFocus: true, // Prevents dismissing of toast on hover
        escapeMarkup: false // Allows HTML in the text
    }).showToast();
};


export const showConfirmDialog = async (title, text) => {
    const result = await Swal.fire({
        title,
        text,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        reverseButtons: true
    });
    return result.isConfirmed;
};

export const showEditDialog = async (currentText) => {
    const result = await Swal.fire({
        title: 'Edit Post',
        input: 'textarea',
        inputValue: currentText,
        inputPlaceholder: 'Type your updated post here...',
        showCancelButton: true,
        confirmButtonText: 'Update',
        cancelButtonText: 'Cancel',
        inputValidator: (value) => {
            if (!value.trim()) {
                return 'Post content cannot be empty!';
            }
        }
    });
    return result.value;
};

export const showCommentDialog = async () => {
    const result = await Swal.fire({
        title: 'Add Comment',
        input: 'textarea',
        inputPlaceholder: 'Type your comment here...',
        showCancelButton: true,
        confirmButtonText: 'Add Comment',
        cancelButtonText: 'Cancel',
        inputValidator: (value) => {
            if (!value.trim()) {
                return 'Comment content cannot be empty!';
            }
        }
    });
    return result.value;
};
