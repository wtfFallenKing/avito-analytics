import React, { ChangeEvent, useRef } from 'react';
import { Button, useRefresh } from 'react-admin';

import FileUploadIcon from '@mui/icons-material/FileUpload';

interface UploadButtonProps {
  onUpload: (file: File) => Promise<boolean>;
}

function UploadButton({ onUpload }: UploadButtonProps) {
  const ref = useRef<HTMLInputElement>(null);
  const refresh = useRefresh();

  const onInput = async (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const [file] = e.target.files;
      if (file.type == 'application/vnd.ms-excel' || file.type == 'text/csv') {
        await onUpload(file);
        refresh();
      }
    }
  };

  return (
    <>
      <input
        ref={ref}
        type="file"
        style={{
          display: 'none',
        }}
        onInput={onInput}
      />
      <Button
        label="Загрузить CSV"
        startIcon={<FileUploadIcon />}
        onClick={() => {
          ref.current?.click();
        }}
      />
    </>
  );
}

export default UploadButton;
