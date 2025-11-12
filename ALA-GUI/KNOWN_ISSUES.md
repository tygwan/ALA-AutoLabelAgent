# Known Issues

## PyQt6 DLL Loading Issue on Windows

**Status**: Open
**Severity**: Medium
**Affects**: Windows environment, GUI tests
**Date Discovered**: 2025-01-13

### Description
PyQt6 fails to import on Windows with the error:
```
ImportError: DLL load failed while importing QtCore: ������ ���ν����� ã�� �� �����ϴ�.
```

This prevents:
- Running GUI-dependent tests (pytest-qt)
- Running the main application GUI
- GUI development and testing

### Environment
- OS: Windows
- Python: 3.9.13
- PyQt6: 6.6.1
- PyQt6-Qt6: 6.10.0

### Workaround
For now, we can:
1. Run non-GUI tests using: `pytest -p no:pytest-qt tests/test_basic.py`
2. Temporarily disable qt_api in pytest.ini
3. Develop and test on Linux/Mac environments
4. Use Windows Subsystem for Linux (WSL)

### Potential Solutions
1. **Install Visual C++ Redistributable**:
   - Download and install Microsoft Visual C++ Redistributable
   - https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

2. **Try PyQt5 instead**:
   - Downgrade to PyQt5 if compatibility issues persist
   - Update requirements.txt and code

3. **Use conda environment**:
   - Try creating conda environment instead of venv
   - conda may handle DLL dependencies better

4. **Check PATH environment**:
   - Ensure Qt DLLs are in PATH
   - Add PyQt6 Qt6 bin directory to PATH

### References
- Similar issues: https://github.com/pytest-dev/pytest-qt/issues
- PyQt6 Windows issues: https://www.riverbankcomputing.com/pipermail/pyqt/

### Next Steps
- Try installing Visual C++ Redistributable
- Test on different Windows machine
- Consider WSL for development
- Update this document when resolved

---
**Last Updated**: 2025-01-13
