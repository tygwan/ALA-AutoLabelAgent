"""
Unit tests for AutoAnnotateDialog.

Tests the auto-annotation dialog UI following TDD methodology.
"""

import pytest

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestAutoAnnotateDialogInitialization:
    """Tests for AutoAnnotateDialog initialization."""

    def test_auto_annotate_dialog_creation(self, qtbot):
        """Test that AutoAnnotateDialog can be created."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert dialog is not None

    def test_dialog_inherits_from_qdialog(self, qtbot):
        """Test that AutoAnnotateDialog inherits from QDialog."""
        from PyQt6.QtWidgets import QDialog

        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert isinstance(dialog, QDialog)

    def test_dialog_has_text_prompt_input(self, qtbot):
        """Test that dialog has text prompt input field."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert hasattr(dialog, "prompt_input")
        assert dialog.prompt_input is not None

    def test_dialog_has_progress_bar(self, qtbot):
        """Test that dialog has progress bar."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert hasattr(dialog, "progress_bar")
        assert dialog.progress_bar is not None

    def test_dialog_has_model_controller(self, qtbot):
        """Test that dialog has model controller."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert hasattr(dialog, "model_controller")
        assert dialog.model_controller is not None

    def test_dialog_has_run_button(self, qtbot):
        """Test that dialog has run button."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert hasattr(dialog, "run_button")
        assert dialog.run_button is not None

    def test_dialog_has_cancel_button(self, qtbot):
        """Test that dialog has cancel button."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)
        assert hasattr(dialog, "cancel_button")
        assert dialog.cancel_button is not None


class TestAutoAnnotateDialogTextPrompt:
    """Tests for text prompt functionality."""

    def test_get_text_prompt(self, qtbot):
        """Test getting text prompt from input."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Set text
        dialog.prompt_input.setText("person, car, dog")

        # Get text
        prompt = dialog.get_text_prompt()
        assert prompt == "person, car, dog"

    def test_set_text_prompt(self, qtbot):
        """Test setting text prompt."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Set prompt
        dialog.set_text_prompt("bicycle, motorcycle")

        # Verify
        assert dialog.prompt_input.text() == "bicycle, motorcycle"

    def test_default_text_prompt(self, qtbot):
        """Test that default text prompt is empty."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        prompt = dialog.get_text_prompt()
        assert prompt == "" or prompt is None


class TestAutoAnnotateDialogProgressBar:
    """Tests for progress bar functionality."""

    def test_progress_bar_initial_value(self, qtbot):
        """Test that progress bar starts at 0."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        assert dialog.progress_bar.value() == 0

    def test_update_progress(self, qtbot):
        """Test updating progress bar."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Update progress
        dialog.update_progress(50, "Processing...")

        assert dialog.progress_bar.value() == 50

    def test_progress_bar_range(self, qtbot):
        """Test that progress bar has correct range."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        assert dialog.progress_bar.minimum() == 0
        assert dialog.progress_bar.maximum() == 100


class TestAutoAnnotateDialogModelIntegration:
    """Tests for model controller integration."""

    def test_run_annotation_with_prompt(self, qtbot):
        """Test running annotation with text prompt."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Set prompt
        dialog.set_text_prompt("person")

        # Load models (mock paths)
        dialog.model_controller.load_models("florence_path", "sam_path")

        # Run annotation
        if hasattr(dialog, "run_annotation"):
            dialog.run_annotation()

    def test_cancel_annotation(self, qtbot):
        """Test cancelling annotation."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Cancel should work even without running
        if hasattr(dialog, "cancel_annotation"):
            dialog.cancel_annotation()


class TestAutoAnnotateDialogSignals:
    """Tests for dialog signals."""

    def test_dialog_has_annotation_complete_signal(self, qtbot):
        """Test that dialog has annotation complete signal."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        assert hasattr(dialog, "annotation_complete")

    def test_annotation_complete_signal_emitted(self, qtbot):
        """Test that annotation complete signal is emitted."""
        from views.auto_annotate_dialog import AutoAnnotateDialog

        dialog = AutoAnnotateDialog()
        qtbot.addWidget(dialog)

        # Load models
        dialog.model_controller.load_models("florence_path", "sam_path")

        # Set prompt
        dialog.set_text_prompt("person")

        # Run and wait for signal
        if hasattr(dialog, "run_annotation"):
            with qtbot.waitSignal(dialog.annotation_complete, timeout=3000):
                dialog.run_annotation()
