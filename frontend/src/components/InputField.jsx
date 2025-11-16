import React from 'react';

export default function InputField({label, ...props}) {
  return (
    <label className="input-label">
      <div className="input-label-text">{label}</div>
      <input className="input-field" {...props} />
    </label>
  );
}
